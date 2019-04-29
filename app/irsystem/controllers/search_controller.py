from . import *
from app.irsystem.controllers.tfidf import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Museum Recomendations"
net_id = "Kevin Tian(kt474), Alex Zhou(az246), Noah Beller(nbb42), Aaron Bu(acb256)"


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    version = request.args.get('version')
    us_only = request.args.get('USonly')
    if version == "old":
        data = range(5)
        more_info = [['', ''], ['', ''], ['', '']]
        output_message = "You searched for: " + query
        # results = get_suggestions(query)
        results = OLD_get_suggestions(query)
    else:
        if not query:
            data = []
            output_message = ''
            more_info = ''
            results = []
        else:
            output_message = query

            results = get_suggestions(query,us_only)
            try:
                more_info = museum_match(results[0][0])
            except IndexError:
                more_info = ''
            #results = museum_match(query)
            # if results[0][0] is None:
            #     more_info = ''
            # if museum_match(results[0][0]) is None:
            #     more_info = ''
            # else:
            #     more_info = museum_match(results[0][0])[0][0]
            #     more_info2 = museum_match(results[0][0])[1][0]
            #     more_info3 = museum_match(results[0][0])[2][0]
            #     more_info4 = museum_match(results[0][0])[3][0]
            #     more_info5 = museum_match(results[0][0])[4][0]

            # top_result = " " + str(get_suggestions(query)[0][0])
            # description = " " + str(get_suggestions(query)[0][2])
            # other_results = " " + str(get_suggestions(query)[1][0])
            data = range(5)

    return render_template('search.html',
                           name=project_name,
                           netid=net_id,
                           output_message=output_message,
                           data=data,
                           results=results,
                           more_info=more_info)
