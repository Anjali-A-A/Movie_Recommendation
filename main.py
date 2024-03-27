from flask import Flask,render_template,request
import pandas as pd
import pickle
app=Flask(__name__)

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))


#streamlit code``
#*********************************************************************

def recommend(movie):
    movie_index=movies[movies['name']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]][1])
    return recommended_movies
        # print(movies.iloc[i[0]][1])

#********************************************************************

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/', methods=['GET','POST'])

def recommendation():
    movie_list = movies['name'].values
    status = False
    recommended_movies_name = []  # Default value for recommended_movies_name

    try:
        if request.form:
            selected_movie = request.form['movies']  # Corrected line
            recommended_movies_name = recommend(selected_movie)
            status = True

            return render_template("index.html", recommended_movies_name=recommended_movies_name, movie_list=movie_list, status=status)

    except Exception as e:
        error = {'error': e}
        return render_template("index.html", error=error, movie_list=movie_list, status=status)

    # Provide a default return statement if the form is not submitted
    return render_template("index.html", movie_list=movie_list, status=status, recommended_movies_name=recommended_movies_name)



if __name__=='__main__':
    app.run(debug=True)