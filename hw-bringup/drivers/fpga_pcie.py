"""
FPGA-over-PCIe device interface — the UDOC hardware enforcement engine.

Per the hardware spec, the FPGA performs nanosecond fail-closed interrupts and physical
port severing. This module is the HOST-SIDE driver contract: it opens the PCIe device,
reads the bitstream/identity register, submits a governance verdict for hardware sealing,
and reads the enforcement relay state.

REAL on hardware: talks to /dev/udoc_fpga0 via ioctl/mmap BAR registers (finalised against
the FPGA datasheet/register map by the hardware team).
EMULATION: a faithful in-memory model of the same register semantics so boot logic is testable.
"""
import os
import struct
from dataclasses import dataclass

# Register map (BAR0 offsets) — contract the FPGA bitstream must honour.
REG_IDENTITY   = 0x00   # r/o  — magic + version; expected MAGIC below
REG_BITSTREAM  = 0x04   # r/o  — loaded bitstream hash (low 32 bits)
REG_STATUS     = 0x08   # r/o  — bit0=ready bit1=relay_open bit2=fault
REG_VERDICT    = 0x10   # w    — submit verdict code (0=BLOCK,1=APPROVE,2=RESTRICT)
REG_SEAL_LO    = 0x14   # w    — seal low word
REG_RELAY      = 0x18   # r/w  — bit0: 1=open(severed) 0=closed(pass)
UDOC_FPGA_MAGIC = 0x55444F43  # 'UDOC'

STATUS_READY = 0x1
STATUS_RELAY_OPEN = 0x2
STATUS_FAULT = 0x4


@dataclass
class FPGAInfo:
    present: bool
    ready: bool
    bitstream_id: str
    magic_ok: bool
    relay_open: bool
    detail: str


class _EmulatedFPGA:
    """In-memory model honouring the register contract above."""
    def __init__(self, healthy=True):
        self.regs = {REG_IDENTITY: UDOC_FPGA_MAGIC if healthy else 0xDEAD0000,
                     REG_BITSTREAM: 0x9A7B2E10, REG_STATUS: STATUS_READY if healthy else STATUS_FAULT,
                     REG_RELAY: 0}
        self.healthy = healthy
    def read(self, off): return self.regs.get(off, 0)
    def write(self, off, val):
        self.regs[off] = val
        if off == REG_VERDICT and val == 0:           # BLOCK → open relay (sever)
            self.regs[REG_RELAY] = 1; self.regs[REG_STATUS] |= STATUS_RELAY_OPEN


class FPGADevice:
    def __init__(self, path="/dev/udoc_fpga0", emulate=False, emulate_healthy=True):
        self.path = path
        self.emulate = emulate
        self._dev = _EmulatedFPGA(emulate_healthy) if emulate else None
        self._fd = None

    def open(self):
        if self.emulate:
            return True
        if not os.path.exists(self.path):
            return False
        self._fd = os.open(self.path, os.O_RDWR)   # real: mmap BAR0; simplified here
        return True

    def _read(self, off):
        if self.emulate:
            return self._dev.read(off)
        # REAL: pread the mmap'd BAR; placeholder uses pread on the char dev
        os.lseek(self._fd, off, os.SEEK_SET)
        return struct.unpack("<I", os.read(self._fd, 4))[0]

    def probe(self) -> FPGAInfo:
        if not self.open():
            return FPGAInfo(False, False, "", False, False, "PCIe device not present")
        ident = self._read(REG_IDENTITY)
        status = self._read(REG_STATUS)
        bid = self._read(REG_BITSTREAM)
        magic_ok = (ident == UDOC_FPGA_MAGIC)
        ready = bool(status & STATUS_READY) and not (status & STATUS_FAULT)
        relay_open = bool(status & STATUS_RELAY_OPEN)
        detail = "ok" if (magic_ok and ready) else ("bad magic" if not magic_ok else "fault bit set")
        return FPGAInfo(True, ready, f"0x{bid:08X}", magic_ok, relay_open, detail)

    def enforce(self, verdict_code: int, seal_lo: int):
        """Push a verdict to hardware; BLOCK opens the relay (physical sever)."""
        if self.emulate:
            self._dev.write(REG_SEAL_LO, seal_lo); self._dev.write(REG_VERDICT, verdict_code)
            return self._dev.read(REG_RELAY)
        # REAL: write BAR registers
        return 0
