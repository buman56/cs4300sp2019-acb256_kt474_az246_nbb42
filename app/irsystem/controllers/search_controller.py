from . import *  
from app.irsystem.controllers.tfidf import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Museum Recomendations"
net_id = "Kevin Tian(kt474), Alex Zhou(az246), Noah Beller(nbb42), Aaron Bu(acb256)"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	results = get_suggestions(query)
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "You searched for: " + query
		# top_result = " " + str(get_suggestions(query)[0][0]) 
		# description = " " + str(get_suggestions(query)[0][2]) 
		# other_results = " " + str(get_suggestions(query)[1][0]) 
		data = range(5)

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, results = results)



