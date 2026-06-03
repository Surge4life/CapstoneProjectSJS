export interface Decision { model_id:string; decision:string; svs:number; risk:number;
  sovereign:boolean; latency_ms:number; within_budget:boolean; seal:string; block_reasons:string[]; }
export interface LoopSnapshot { seths_placed:number; ts_monthly_profit:number;
  madiba_cumulative_recycled:number; udoc_decisions:number; loop:string; }
