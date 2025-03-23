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
from datetime import timedelta, datetime

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
                    # self._execute_trading_strategy()
                    self.test()
                    time.sleep(60)
                    self.stop()
                except Exception as inner_error:
                    self.logger.error(f"Error in automated handler thread: {inner_error}")
        
        except Exception as outer_error:
            self.logger.error(f"Automated handler thread failed: {outer_error}")
        
        finally:
            self.logger.info(f"Automated handler thread {self.automated_handler_id} stopped")

    def test(self):
        try:
            predictions = (self.db_session.query(Prediction).filter(Prediction.symbol == 'XAUUSD', Prediction.is_deleted == False).order_by(Prediction.date.asc()).all())
            minute_data = pd.read_csv('/home/sheldor/Documents/thesis/thesis/app/automation_handler/data_1m.csv')
            minute_data = minute_data[['datetime', 'close']]
            
            minute_data['datetime'] = pd.to_datetime(minute_data['datetime'])
            next_prediction = predictions[0]
            current_miniute = minute_data.iloc[0]

            # Ensure next_prediction.date is a datetime object
            if isinstance(next_prediction.date, str):
                next_prediction.date = datetime.strptime(next_prediction.date, '%Y-%m-%d %H:%M:%S')
            current_miniute_index = 0 
            current_prediction_index = 0
            pred_len = len(predictions)
            print(pred_len)
            minute_data_len = len(minute_data)
            
            print(minute_data_len)
            print(type (next_prediction.date))
            print(type (current_miniute['datetime']))
            automated_handler = (
            self.db_session.query(AutomatedHandler)
            .filter(AutomatedHandler.id == self.automated_handler_id)
            .first()
            )
            symbol = automated_handler.symbol
            print("symbol ", symbol)
            stock = (self.db_session.query(Stock).filter(Stock.symbol == symbol).first())
            stock_id = stock.id
            account = (self.db_session.query(Account).filter(Account.id == self.account_id).first())
            automated_account = (self.db_session.query(AutomatedAccount).filter(AutomatedAccount.account_id == self.account_id).first())
            while(next_prediction.date > current_miniute['datetime']):
                if( current_miniute_index == minute_data_len - 1 or current_prediction_index == pred_len - 1):
                    print("breaking the loop ")
                    break
                print("start of the loop ")
                self.db_session.commit()
                # getting only one for now 
                trade = (self.db_session.query(Trade).filter(Trade.stock_id == stock_id, Trade.user_id == self.user_id, Trade.is_Automated == True, Trade.trade_status == 'OPEN').first())
                if trade:
                    print("there is a trade so closing it in handler_closing  ")
                    # self._handle_closing_trade(account, automated_account, trade, stock)
                    # write a function for closing trade
                    # Close the trade
                    if( next_prediction.closing_price < current_miniute['close'] and trade.trade_start_price < current_miniute['close']):
                        print(" closing the trade  in the first condition ")
                        trade.trade_end_price = current_miniute['close']
                        trade.trade_end_date = current_miniute['datetime']
                        trade.trade_status = 'CLOSED'
                        profit = (trade.trade_end_price - trade.trade_start_price) * trade.quantity * (trade.trade_type == "LONG" and 1 or -1)
                        selling_price = trade.trade_end_price * trade.quantity
                        trade.trade_profit = profit
                        trade.updated_by = self.user_id
                        # profit = profit + selling_price
                        automated_account.balance = automated_account.balance + selling_price
                        account.automated_balance = account.automated_balance + selling_price
                        transaction = Transaction(
                            account_id = account.id,
                            amount = profit,
                            symbol = stock.symbol,
                            transaction_type = 'CREDIT',
                            transaction_date = current_miniute['datetime'],
                            transaction_status = 'DONE',    
                            transaction_done_by = 'AUTOMATED',
                            created_by = self.user_id
                        )
                        self.db_session.add(transaction)
                        self.db_session.commit()
                        print("closed a trade")
                        # break 
                    elif next_prediction.closing_price > current_miniute['close'] and trade.trade_start_price < current_miniute['close'] and next_prediction.prediction_direction == False:
                        print("closing the trade in the second condition ")
                        trade.trade_end_price = current_miniute['close']
                        trade.trade_end_date = current_miniute['datetime']
                        trade.trade_status = 'CLOSED'
                        profit = (trade.trade_end_price - trade.trade_start_price) * trade.quantity * (trade.trade_type == "LONG" and 1 or -1)
                        selling_price = trade.trade_end_price * trade.quantity
                        trade.trade_profit = profit
                        trade.updated_by = self.user_id
                        # profit = profit + selling_price
                        automated_account.balance = automated_account.balance + selling_price
                        account.automated_balance = account.automated_balance + selling_price
                        transaction = Transaction(
                            account_id = account.id,
                            amount = profit,
                            symbol = stock.symbol,
                            transaction_type = 'CREDIT',
                            transaction_date = current_miniute['datetime'],
                            transaction_status = 'DONE',    
                            transaction_done_by = 'AUTOMATED',
                            created_by = self.user_id
                        )
                        self.db_session.add(transaction)
                        self.db_session.commit()
                        print("closed a trade")
                        # break 
                        
                    next_minute = minute_data.iloc[current_miniute_index+1]
                    if( next_minute['datetime'] < next_prediction.date):
                        print("condition did not met so increamenting the index  in first if ")
                        current_miniute_index += 1
                        current_miniute = minute_data.iloc[current_miniute_index]
                        
                    else:
                        print("increamenting both ")
                        current_miniute_index += 1
                        current_miniute = minute_data.iloc[current_miniute_index]
                        current_prediction_index += 1
                        next_prediction = predictions[current_prediction_index]
                    
                else : 
                    print("there is no trade so opening one ")
                    #place the trade
                    if(next_prediction.prediction_direction == True):
                        if(next_prediction.closing_price > current_miniute['close']):
                            # budget = 20000
                            budget = automated_account.balance 
                            automated_account.balance -= budget
                            # automated_account.save()
                            account.automated_balance -= budget
                            current_price_float = float(current_miniute['close'])
                            current_datetime = current_miniute['datetime']
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

                        

                    next_minute = minute_data.iloc[current_miniute_index+1]
                    
                    if( next_minute['datetime'] < next_prediction.date):
                        current_miniute_index += 1
                        current_miniute = minute_data.iloc[current_miniute_index]
                        print("current_miniute ", current_miniute)
                    else:
                        print("increamenting both ")
                        current_miniute_index += 1
                        current_miniute = minute_data.iloc[current_miniute_index]
                        current_prediction_index += 1
                        next_prediction = predictions[current_prediction_index]
                
                print("In the loop ")
                
            # print(minitue_data)
           
                # print(prediction.closing_price)
            
        except Exception as e:
            self.logger.error(f"Error in automated handler thread: {e}")

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
            trade = (self.db_session.query(Trade).filter(Trade.stock_id == stock.id, Trade.user_id == self.user_id, Trade.is_Automated == True, Trade.trade_status == 'OPEN').first())
            # self._trade( account, automated_account, stock )
            if trade:
                print("there is a trade so closing it in handler_closing  ")
                self._handle_closing_trade(account, automated_account, trade, stock)
            else :
                self._trade( account, automated_account, stock )
            
            self.stop()
        except Exception as e:
            self.logger.error(f"Trading strategy execution error: {e}")

    def _handle_closing_trade(self, account, automated_account, trade, stock):
        try:

            # while(True): 
                # Close the trade
                # Get the current price
                current_price_csv = self.get_current_price(symbol = stock.symbol, exchange = 'FOREXCOM', interval = 15, n_bars=10)
                if not isinstance(current_price_csv, pd.DataFrame):
                    current_price_csv = pd.DataFrame(current_price_csv)
                current_price_csv_reset = current_price_csv.reset_index()
                current_price = current_price_csv_reset['close'].iloc[-1]
                current_datetime = current_price_csv_reset['datetime'].iloc[-1]
                predictions = (self.db_session.query(Prediction).filter(Prediction.symbol == stock.symbol, Prediction.is_deleted == False).order_by(Prediction.date.desc()).all())
                prediction = predictions[0] if predictions else None
                print("before if prediction not ")
                if not prediction:
                    # break
                    pass
                print(prediction.date)
                print(current_datetime)
                if prediction.date < current_datetime:
                    # continue
                    print("need new prediction")
            
                prediction_price = float(prediction.closing_price)
                print("prediction_price ", prediction_price)
                print("current_price ", current_price)
                print("trade.trade_start_price ", trade.trade_start_price)
                if prediction_price < current_price and trade.trade_start_price < current_price :
                    print("prediction_price < current_price and trade.trade_start_price > current_price ")
                    # Close the trade
                    trade.trade_end_price = current_price
                    trade.trade_end_date = current_datetime
                    trade.trade_status = 'CLOSED'
                    profit = (trade.trade_end_price - trade.trade_start_price) * trade.quantity * (trade.trade_type == "LONG" and 1 or -1)
                    selling_price = trade.trade_end_price * trade.quantity
                    trade.trade_profit = profit
                    trade.updated_by = self.user_id
                    profit = profit + selling_price
                    automated_account.balance = automated_account.balance + profit
                    account.automated_balance = account.automated_balance + profit
                    transaction = Transaction(
                        account_id = account.id,
                        amount = profit,
                        symbol = stock.symbol,
                        transaction_type = 'CREDIT',
                        transaction_date = current_datetime,
                        transaction_status = 'DONE',    
                        transaction_done_by = 'AUTOMATED',
                        created_by = self.user_id
                    )
                    self.db_session.add(transaction)
                    self.db_session.commit()


                    pass
                elif prediction_price > current_price and trade.trade_start_price < current_price and prediction.prediction_direction == False:
                    # Close the trade
                    print("prediction_price > current_price and trade.trade_start_price < current_price and prediction.prediction_direction == False ")
                    print("second if ")
                    trade.trade_end_price = current_price
                    trade.trade_end_date = current_datetime
                    trade.trade_status = 'CLOSED'
                    profit = (trade.trade_end_price - trade.trade_start_price) * trade.quantity * (trade.trade_type == "LONG" and 1 or -1)
                    selling_price = trade.trade_end_price * trade.quantity
                    trade.trade_profit = profit
                    trade.updated_by = self.user_id
                    profit = profit + selling_price
                    automated_account.balance = automated_account.balance + profit
                    account.automated_balance = account.automated_balance + profit
                    transaction = Transaction(
                        account_id = account.id,
                        amount = profit,
                        symbol = stock.symbol,
                        transaction_type = 'CREDIT',
                        transaction_date = current_datetime,
                        transaction_status = 'DONE',    
                        transaction_done_by = 'AUTOMATED',
                        created_by = self.user_id
                    )
                    self.db_session.add(transaction)
                    self.db_session.commit()
                   
                    pass
                        
            
        except Exception as e:
            self.logger.error(f"Trade closing error: {e}")

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