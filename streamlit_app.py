import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

class ArbitrageCalculator:
    def __init__(self):
        self.treasury_rate = 0.044
        self.sol_staking_rate = 0.057
        self.sol_borrow_apr = 0.0246
        self.usdc_supply_apr = 0.0993
        self.ltv_ratio = 0.75
        self.sol_price = 211.06

    def calculate_returns(self, initial_capital, usdc_conversion_pct, sol_borrow_pct):
        if usdc_conversion_pct > 100:
            return "Error: USDC conversion cannot exceed 100%"
            
        # Step 1: Convert USD to USDC
        usdc_amount = initial_capital * (usdc_conversion_pct / 100)
        remaining_usd = initial_capital - usdc_amount
        treasury_return = remaining_usd * self.treasury_rate
        
        # Step 2: Lend USDC to Solend
        usdc_lending_return = usdc_amount * self.usdc_supply_apr
        
        # Step 3: Borrow SOL
        max_sol_borrow_usd = usdc_amount * self.ltv_ratio
        actual_sol_borrow_usd = max_sol_borrow_usd * (sol_borrow_pct / 100)
        sol_borrow_quantity = actual_sol_borrow_usd / self.sol_price
        sol_borrowing_cost = actual_sol_borrow_usd * self.sol_borrow_apr
        
        # Step 4: Stake borrowed SOL
        sol_staking_return = actual_sol_borrow_usd * self.sol_staking_rate
        
        total_return = (
            treasury_return +
            usdc_lending_return +
            sol_staking_return -
            sol_borrowing_cost
        )
        
        net_apr = (total_return / initial_capital) * 100
        
        return {
            'Initial Capital': f"${initial_capital:,.2f}",
            'Step 1: USD Allocation': {
                'USDC Converted': f"${usdc_amount:,.2f}",
                'Remaining USD': f"${remaining_usd:,.2f}",
                'Treasury Return (4.4% APR)': f"${treasury_return:,.2f}"
            },
            'Step 2: USDC Lending': {
                'USDC Lent to Solend': f"${usdc_amount:,.2f}",
                'Lending Return (9.93% APR)': f"${usdc_lending_return:,.2f}"
            },
            'Step 3: SOL Borrowing': {
                'Maximum Borrowing Power': f"${max_sol_borrow_usd:,.2f}",
                'Actual SOL Borrowed': f"${actual_sol_borrow_usd:,.2f} (≈{sol_borrow_quantity:.2f} SOL)",
                'Borrowing Cost (2.46% APR)': f"${sol_borrowing_cost:,.2f}"
            },
            'Step 4: SOL Staking': {
                'SOL Staked in Coinbase': f"${actual_sol_borrow_usd:,.2f} (≈{sol_borrow_quantity:.2f} SOL)",
                'Staking Return (5.7% APY)': f"${sol_staking_return:,.2f}"
            },
            'Returns Summary': {
                'Treasury Return': f"${treasury_return:,.2f}",
                'USDC Lending Return': f"${usdc_lending_return:,.2f}",
                'SOL Staking Return': f"${sol_staking_return:,.2f}",
                'SOL Borrowing Cost': f"-${sol_borrowing_cost:,.2f}",
                'Total Annual Return': f"${total_return:,.2f}",
                'Net APR': f"{net_apr:.2f}%"
            }
        }

def main():
    st.set_page_config(
        page_title="Arbitrage Calculator",
        page_icon="💰",
        layout="wide"
    )

    st.title("💰 DeFi Arbitrage Calculator (Lending/Borrow)")
    
    # Add description
    st.markdown("""
    This calculator helps you analyze potential returns from a multi-step DeFi arbitrage strategy:
    1. Convert USD to USDC (remaining USD earns 4.4% APR)
    2. Lend USDC to Solend (earn 9.93% APR)
    3. Borrow SOL against USDC collateral
    4. Stake borrowed SOL in Coinbase (earn 5.7% APY)
    """)

    # Create two columns for input
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Initial Setup")
        initial_capital = st.number_input(
            "Initial Capital ($)",
            min_value=100,
            max_value=1000000,
            value=1000,
            step=100
        )

        usdc_conversion_pct = st.slider(
            "Step 1: USD to USDC Conversion (%)",
            min_value=0,
            max_value=100,
            value=60
        )

        sol_borrow_pct = st.slider(
            "Step 3: SOL Borrowing (%)",
            min_value=0,
            max_value=100,
            value=75
        )

    # Calculate returns
    calculator = ArbitrageCalculator()
    results = calculator.calculate_returns(
        initial_capital=initial_capital,
        usdc_conversion_pct=usdc_conversion_pct,
        sol_borrow_pct=sol_borrow_pct
    )

    # Display results in the second column
    with col2:
        st.subheader("Results")
        for section, data in results.items():
            if section == 'Initial Capital':
                continue
            with st.expander(section, expanded=True):
                if isinstance(data, dict):
                    for key, value in data.items():
                        st.write(f"{key}: {value}")
                else:
                    st.write(data)

if __name__ == "__main__":
    main()