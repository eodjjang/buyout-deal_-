"""Fixed cell addresses shared across builders (single source of truth)."""
from __future__ import annotations

SHEET_README = "0_README"
SHEET_INPUT = "1_Input_BaseCase"
SHEET_STRESS = "2_Stress_Panel"
SHEET_OVERLAY = "3_Operating_Overlay"
SHEET_DEBT = "4_Debt_Schedule"
SHEET_WATERFALL = "5_CF_Waterfall"
SHEET_DCF = "6_DCF_Valuation"
SHEET_RETURNS = "7_Returns_LTV"
SHEET_DASH = "8_Dashboard"
SHEET_9A = "9a_CIQ_Trading_Raw"
SHEET_9B = "9b_CIQ_Transaction_Raw"
SHEET_9C = "9c_Manual_Supplement"
SHEET_PEER = "9_Peer_Summary"

ALL_SHEETS = [
    SHEET_README,
    SHEET_INPUT,
    SHEET_STRESS,
    SHEET_OVERLAY,
    SHEET_DEBT,
    SHEET_WATERFALL,
    SHEET_DCF,
    SHEET_RETURNS,
    SHEET_DASH,
    SHEET_9A,
    SHEET_9B,
    SHEET_9C,
    SHEET_PEER,
]

# 2_Stress_Panel Case_Switch anchor (design §2.1)
CASE_SWITCH_CELL = "B3"

# 9a/9b paste ranges (design §9a, §9b)
S9A_HEADER_ROW = 1
S9A_TICKER_START = "A2"
S9A_DATA_START = "B2"
S9A_DATA_END_ROW = 101  # max 100 peer rows

S9B_HEADER_ROW = 1
S9B_DATA_START = "A2"
S9B_DATA_END_ROW = 501  # max 500 transaction rows (design v0.4)
