import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app\serger_log.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
	global model
	# load the pre-trained model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)
	
modelpath = "app\models\model.dill"	
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process."""


@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		df = flask.request.get_json()
		df = pd.DataFrame(pd.read_json(df, orient='split'))
		logger.info(f'{dt} Accepted packages: {df.shape[0]}')
		try:
			preds = model.predict_proba(df)
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			return flask.jsonify(str(e))

		# indicate that the request was a success
		data["predictions"] = preds[:, 1].tolist()
		data["success"] = True
		logger.info(f'{dt} Packages sent: {len(data["predictions"])}')

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
# python app\server.py
if __name__ == "__main__":
	print(("*** Loading the model and Flask starting server ***\n"
			"*** please wait until server has fully started ***"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)