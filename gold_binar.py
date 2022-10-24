from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import pandas as pd
import sqlite3

con = sqlite3.connect("Gold_Binar.db")
cur = con.cursor()
df = pd.read_sql_query("SELECT * FROM Data", con)
abusive = pd.read_sql_query("SELECT * FROM Abusive", con)
list_alay = pd.read_sql_query("SELECT * FROM new_kamusalay", con)

con.close()

###############################################################################################################
app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda:'1.0.0'),
        'description': LazyString(lambda:'Dokumentasi API untuk Data Processing dan Modeling')
        }, host = LazyString(lambda: request.host)
    )
swagger_config = {
        "headers":[],
        "specs":[
            {
            "endpoint":'docs',
            "route":'/docs.json'
            }
        ],
        "static_url_path":"/flasgger_static",
        "swagger_ui":True,
        "specs_route":"/docs/"
    }
swagger = Swagger(app, template=swagger_template, config=swagger_config)

##############################################################################################################
con = sqlite3.connect("Gold_Binar.db")
cur = con.cursor()

df = pd.DataFrame(df, columns = ['Tweet'])

df['id'] = range(0,len(df))
df['id'] = df['id'].astype('int')
df.index = df['id']

def frame(df,abusive):
    df_get = df.copy()
    df_get['new_tweet'] = df_get['Tweet'].str.lower().tolist()
    list_tweet = df_get['new_tweet'].tolist()
    for i in list_tweet:
        for j in abusive:
            if j in i :
                k = list_tweet[list_tweet.index(i)].replace(j,'**')
                list_tweet[list_tweet.index(i)] = k
                i = k
    df_get['new_tweet'] = list_tweet
    json = df_get.to_dict(orient='index')

    del df_get
    return json


##############################################################################################################

# GET
@swag_from("docs/index.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})

@swag_from("docs/index.yml", methods=['GET'])
@app.route('/lang', methods=['GET'])
def returnAll():

    json = frame(df)

    return jsonify(json)

###############################################################################################################
# GET
@swag_from("docs/lang_get.yml", methods=['GET'])
@app.route('/lang/<id>', methods=['GET'])
def returnOne(id):
    
    json = frame(df)
    
    id = int(id)
    json = json[id]

    return jsonify(json)

##############################################################################################################
# POST
@swag_from("docs/lang_post.yml", methods=['POST'])
@app.route('/lang', methods=['POST'])
def addOne():
    Tweet = {'Tweet': request.json['Tweet']}
    df.loc[len(df) + 1]=[Tweet['Tweet'],max(df['id'])+1]
    df.index = df['id']

    
    json = frame(df)

    id = max(df.index)
    json = json[id]

    return jsonify(json)

##############################################################################################################
# PUT
# @swag_from("docs/lang_put.yml", methods=['PUT'])
# @app.route('/lang/<id>', methods=['PUT'])
# def editOne(id):
#     Tweet = {'Tweet': request.json['Tweet']}
#     id = int(id)

#     if id in df['id'].tolist():
#         df.loc[id] = [Tweet['Tweet'],id]

#         json = frame(df)

#         json = json[id]

#         return jsonify(json)
#     else :
#         return 'input ulang'

# ###############################################################################################################
# # DELETE
# @swag_from("docs/lang_delete.yml", methods=['DELETE'])
# @app.route('/lang/<id>', methods=['DELETE'])
# def removeOne(id):

#     global df
#     id = int(id)
#     df = df.drop(id)

#     json = frame(df)

#     return jsonify(json)

# ###############################################################################################################

# # @swag_from("docs/lang_upload.yml", methods=['DELETE'])
# # @app.route('/lang', methods=['DELETE'])
# # def removeOne():

# # Cari code flask untuk upload file
# # file nya di baca oleh pandas
# # pandas ekstrak data
# # upload ke DB

# #     return jsonify(json)

###############################################################################################################


if __name__ == "__main__":
    app.run()