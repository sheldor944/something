import logging
import sys
import threading
import time
from sqlalchemy.orm import Session
from models.account import AutomatedHandler, Account, AutomatedAccount, Transaction
from models.stock import Stock
from models.trade import Prediction, Trade
from automation_handler.getLiveData import getLiveData
import pandas as pd
from datetime import timedelta

# Clear existing handlers
logging.getLogger().handlers.clear()

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Prevent log propagation
logging.getLogger().propagate = False

class AutomatedHandlerThread(threading.Thread):
    def __init__(self, db_session, automated_handler_id, user_id, account_id):
        super().__init__()
        
        # Create a unique logger for this thread
        self.logger = logging.getLogger(f'AutomatedHandler-{automated_handler_id}')
        self.logger.propagate = False
        
        # Ensure no duplicate handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.INFO)
        
        # Rest of your initialization...
        self.db_session = db_session
        self.automated_handler_id = automated_handler_id
        self.user_id = user_id
        self.account_id = account_id
        self.is_running = True
        self.daemon = True

    def run(self):
        try:
            self.logger.info(f"Starting automated handler thread for handler {self.automated_handler_id}")
            
            while self.is_running:
                try:
                    self._execute_trading_strategy()
                    time.sleep(60)
                except Exception as inner_error:
                    self.logger.error(f"Error in automated handler thread: {inner_error}")
        
        except Exception as outer_error:
            self.logger.error(f"Automated handler thread failed: {outer_error}")
        
        finally:
            self.logger.info(f"Automated handler thread {self.automated_handler_id} stopped")

    def _execute_trading_strategy(self):
        try:
            self.logger.info("Executing trading strategy")
            # I have db_session, account_id, automated_handler_id, user_id
            # Get the automated handler
            # Fist check for existing trades, then trade for new one. 
            automated_handler = (
                self.db_session.query(AutomatedHandler)
                .filter(AutomatedHandler.id == self.automated_handler_id)
                .first()
            )
            
            symbol = automated_handler.symbol
            print("symbol ", symbol)
            stock = (self.db_session.query(Stock).filter(Stock.symbol == symbol).first())
            # Get the account

            account = (self.db_session.query(Account).filter(Account.id == self.account_id).first())
            
            # Get the automated account
            automated_account = (self.db_session.query(AutomatedAccount).filter(AutomatedAccount.account_id == self.account_id).first())
            
            
            predictions = (self.db_session.query(Prediction).filter(Prediction.symbol == symbol, Prediction.is_deleted == False).order_by(Prediction.date.desc()).all())
            prediction = predictions[0] if predictions else None
            self._trade( account, automated_account, stock )
            
            self.stop()
        except Exception as e:
            self.logger.error(f"Trading strategy execution error: {e}")

    def _trade(self, account, automated_account, stock):
        try:
            # Check if the prediction is profitable
            # while(True):
                
                print("In the trade loop")
                print("stock ", stock.symbol)
                symbol = stock.symbol
                predictions = (self.db_session.query(Prediction).filter(Prediction.symbol == symbol, Prediction.is_deleted == False).order_by(Prediction.date.desc()).all())
                prediction = predictions[0] if predictions else None
                print("before if prediction not ")
                if not prediction:
                    # break
                    pass
                print("got prediction")
                current_price_csv = self.get_current_price(symbol = prediction.symbol, exchange = 'FOREXCOM', interval = 15, n_bars=10)
                if not isinstance(current_price_csv, pd.DataFrame):
                    current_price_csv = pd.DataFrame(current_price_csv)
                print("got current prices csv ")
                current_price_csv_reset = current_price_csv.reset_index()

                current_price = current_price_csv_reset['close'].iloc[-1]
                current_datetime = current_price_csv_reset['datetime'].iloc[-1]
                # current_price = current_price_csv['close'].iloc[-1]
                print("current_price ", current_price)
                # current_datetime = current_price_csv[0].iloc[-1]
                print("current_price ", current_price)
                print("current_datetime ", current_datetime)
                time_difference = prediction.date - current_datetime
                if ( time_difference > timedelta(minutes=14) ): 
                    print("time_difference ", time_difference)
                    if prediction.prediction_direction == True:
                        print("prediction.prediction_direction ", prediction.prediction_direction)
                        print("prediction.closing_price ", prediction.closing_price)
                        print("current_price ", current_price)
                        print(type(current_price))
                        print(type(prediction.closing_price))
                        current_price_float = float(current_price)
                        print(type(current_price_float))
                        prediction_price = float(prediction.closing_price)
                        if prediction_price > current_price_float:
                            print("prediction.closing_price > current_price_float['close'] ", prediction_price, current_price_float)
                            # Buy 
                            budget = automated_account.balance * 0.1
                            automated_account.balance -= budget
                            # automated_account.save()
                            account.automated_balance -= budget
                            # account.save()
                            trade = Trade(
                                stock_id = stock.id,
                                user_id = self.user_id,
                                trade_done_by = 'AUTOMATED',
                                trade_start_price = current_price_float,
                                quantity = budget/current_price_float,
                                trade_start_date = current_datetime,
                                trade_type = 'LONG',
                                trade_status = 'OPEN',
                                is_Automated = True,
                                created_by = self.user_id
                            )
                            transaction = Transaction(
                                account_id = account.id,
                                amount = budget,
                                symbol = stock.symbol,
                                transaction_type = 'DEBIT',
                                transaction_date = current_datetime,
                                transaction_status = 'DONE',
                                transaction_done_by = 'AUTOMATED',
                                created_by = self.user_id
                            )
                            self.db_session.add(transaction)
                            self.db_session.add(trade)
                            self.db_session.commit()
                            # break 
                            pass
                        else:
                            # Do nothing
                            pass
                    elif prediction.signal == 'SELL':
                        # Do nothing for now 
                        pass


                pass 
        except Exception as e:
            self.logger.error(f"Trade execution error: {e}")
    def get_current_price(self, symbol = 'XAUUSD', exchange = 'FOREXCOM', interval = 15, n_bars=10):
        return getLiveData(symbol, exchange, interval, n_bars)

    def stop(self):
        self.is_running = False
        self.logger.info(f"Stopping automated handler thread {self.automated_handler_id}")