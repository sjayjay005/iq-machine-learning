"""
Martingale Trading Strategy Simulator

This module simulates a martingale trading/betting strategy based on a predefined table.
It tracks current capital, bet size, and trade outcomes according to the martingale strategy rules.
"""

import os
import logging
from typing import Dict, Tuple, List, Optional

logger = logging.getLogger(__name__)

# Define the betting table with different target levels
BETTING_TABLE = {
    "$1": {
        "level_1_bet": 1,
        "level_2_bet": 2.5,
        "level_1_profit": 0.8,  # 80% profit on level 1 bet
        "level_2_profit_after_covering_loss": 1,  # Profit after covering level 1 loss
    },
    "$5": {
        "level_1_bet": 5,
        "level_2_bet": 12.5,
        "level_1_profit": 4,  # 80% profit on level 1 bet
        "level_2_profit_after_covering_loss": 5,  # Profit after covering level 1 loss
    },
    "$50": {
        "level_1_bet": 50,
        "level_2_bet": 125,
        "level_1_profit": 40,  # 80% profit on level 1 bet
        "level_2_profit_after_covering_loss": 50,  # Profit after covering level 1 loss
    },
    "$300": {
        "level_1_bet": 300,
        "level_2_bet": 750,
        "level_1_profit": 240,  # 80% profit on level 1 bet
        "level_2_profit_after_covering_loss": 300,  # Profit after covering level 1 loss
    },
}

def get_user_inputs() -> Tuple[float, str, int]:
    """
    Get user inputs for the martingale strategy simulation.
    
    Returns:
        Tuple containing starting capital, target level, and number of trades.
    """
    # Get starting capital
    while True:
        try:
            starting_capital = float(input("Please provide your starting capital: "))
            if starting_capital <= 0:
                print("Starting capital must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for starting capital.")
    
    # Get target level
    while True:
        target_level = input("Please choose a Target Level from the table (e.g., $1, $5, $50, $300): ")
        if target_level not in BETTING_TABLE:
            print(f"Invalid target level. Please choose from: {', '.join(BETTING_TABLE.keys())}")
            continue
        break
    
    # Get number of trades
    while True:
        try:
            num_trades = int(input("How many trades would you like to simulate? "))
            if num_trades <= 0:
                print("Number of trades must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for number of trades.")
    
    return starting_capital, target_level, num_trades

def simulate_martingale_strategy(starting_capital: float, target_level: str, num_trades: int) -> None:
    """
    Simulate the martingale trading strategy.
    
    Args:
        starting_capital: Initial capital for the simulation.
        target_level: Target level from the betting table.
        num_trades: Number of trades to simulate.
    """
    # Initialize variables
    current_capital = starting_capital
    consecutive_losses = 0
    wins = 0
    losses = 0
    current_bet_level = "level_1_bet"
    
    # Get betting parameters for the chosen target level
    betting_params = BETTING_TABLE[target_level]
    
    # Current bet amount starts at level 1
    current_bet_amount = betting_params["level_1_bet"]
    
    # Simulate trades
    for trade_num in range(1, num_trades + 1):
        # Check if we have enough capital for the current bet
        if current_capital < current_bet_amount:
            print(f"\nTrade {trade_num}: INSUFFICIENT CAPITAL")
            print(f"Current Capital: ${current_capital:.2f}")
            print(f"Required Bet: ${current_bet_amount:.2f}")
            print("Simulation stopped: BROKE")
            break
        
        # Display current trade information
        print(f"\nTrade {trade_num}. Current Bet: ${current_bet_amount:.2f}. Current Capital: ${current_capital:.2f}.")
        
        # Get trade outcome from user
        while True:
            outcome = input("What is the outcome (Win/Loss)? ").strip().lower()
            if outcome in ["win", "w"]:
                outcome = "win"
                break
            elif outcome in ["loss", "l"]:
                outcome = "loss"
                break
            else:
                print("Please enter 'Win' or 'Loss' (or 'W' or 'L').")
        
        # Process trade outcome
        if outcome == "win":
            wins += 1
            
            # Calculate profit based on current bet level
            if current_bet_level == "level_1_bet":
                profit = betting_params["level_1_profit"]
                print(f"Trade {trade_num} Outcome: Win. Profit: ${profit:.2f}. New Capital: ${current_capital + profit:.2f}.")
            else:  # level_2_bet
                profit = betting_params["level_2_profit_after_covering_loss"]
                print(f"Trade {trade_num} Outcome: Win. Profit (after covering Level 1 loss): ${profit:.2f}. New Capital: ${current_capital + profit:.2f}.")
            
            # Update capital
            current_capital += profit
            
            # Reset to level 1 bet
            current_bet_level = "level_1_bet"
            current_bet_amount = betting_params["level_1_bet"]
            consecutive_losses = 0
            
            # Display next bet amount
            print(f"Next Bet: ${current_bet_amount:.2f}")
            
        else:  # Loss
            losses += 1
            consecutive_losses += 1
            
            # Update capital
            current_capital -= current_bet_amount
            
            # Display loss information
            print(f"Trade {trade_num} Outcome: Loss. Loss: ${current_bet_amount:.2f}. New Capital: ${current_capital:.2f}. Consecutive Losses: {consecutive_losses}.")
            
            # Move to level 2 bet if at level 1
            if current_bet_level == "level_1_bet":
                current_bet_level = "level_2_bet"
                current_bet_amount = betting_params["level_2_bet"]
            # Stay at level 2 if already there (as per requirements)
            
            # Check if we have enough capital for the next bet
            if current_capital < current_bet_amount:
                print(f"Insufficient capital for next bet (${current_bet_amount:.2f}). Simulation stopped: BROKE")
                break
            
            # Display next bet amount
            print(f"Next Bet: ${current_bet_amount:.2f}")
    
    # Display final summary
    print("\n=== Simulation Summary ===")
    print(f"Total Trades Simulated: {wins + losses}")
    print(f"Starting Capital: ${starting_capital:.2f}")
    print(f"Ending Capital: ${current_capital:.2f}")
    print(f"Net Profit/Loss: ${current_capital - starting_capital:.2f}")
    print(f"Number of Wins: {wins}")
    print(f"Number of Losses: {losses}")
    
    if wins + losses < num_trades:
        print("Reason for Stopping: BROKE (Insufficient capital for next bet)")

def run_strategy():
    """
    Run the martingale strategy simulator.
    """
    print("\n=== Martingale Trading Strategy Simulator ===")
    
    # Get user inputs
    starting_capital, target_level, num_trades = get_user_inputs()
    
    # Run simulation
    simulate_martingale_strategy(starting_capital, target_level, num_trades)
