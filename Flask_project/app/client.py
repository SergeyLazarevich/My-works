import requests
import numpy as np
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
from sklearn.metrics import roc_auc_score, precision_recall_curve

handler = RotatingFileHandler(filename='app\client_log.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# формируем запрос
def send_json(df):
    body = df.to_json(orient='split')
    myurl = "http://192.168.100.77:8180/predict"
    headers = {'content-type': 'application/json; charset=utf-8'}
    response = requests.post(myurl, json=body, headers=headers)
    return response.json()

if __name__ == '__main__':

    X_test = pd.read_csv("./Data Explorer/X_valid.csv")
    y_test = pd.read_csv("./Data Explorer/y_valid.csv")
    
    N = X_test.shape[0]
    y_predic = []
    package = 25

    for i in range(0, (N - package), package):
        dt = strftime("[%Y-%b-%d %H:%M:%S]")
        reply = send_json(X_test.iloc[i: (i + package)])
        logger.info(f'{dt} Packages sent: {package}')
        if reply["success"]:
            y_predic.extend(reply["predictions"])
            logger.info(f'{dt} Accepted packages: {len(reply["predictions"])}')
        else:
            logger.warning(f'{dt} Exception: {reply}')
    
    if N % package:
        dt = strftime("[%Y-%b-%d %H:%M:%S]")
        reply = send_json(X_test.iloc[(N - (N % package)): N])
        logger.info(f'{dt} Packages sent: {N % package}')
        if reply["success"]:
            y_predic.extend(reply["predictions"])
            logger.info(f'{dt} Accepted packages: {len(reply["predictions"])}')
        else:
            logger.warning(f'{dt} Exception: {reply}')


    precision, recall, thresholds = precision_recall_curve(y_test.values[:len(y_predic)], y_predic)

    fscore = (2 * precision * recall) / (precision + recall)
    # locate the index of the largest f score
    ix = np.argmax(fscore)
    print(f'Best Threshold={thresholds[ix]}, F-Score={fscore[ix]:.3f}, Precision={precision[ix]:.3f}, Recall={recall[ix]:.3f}')
    print(f'roc_auc= {roc_auc_score(y_score=y_predic, y_true=y_test.values[:len(y_predic)])}')