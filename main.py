import streamlit as st
import pickle
import pandas as pd
import requests
import time
from PIL import Image

# video_file = open("gunday.mp4", "rb")
# video_bytes = video_file.read()
# st.video(video_bytes)

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=1fdb70c5fa74b7c01ecfd0c31d2f1d1c&&language=en%20US".format(movie_id))

    data=response.json()
   
 
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']




def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movie=[]
    recommend_movie_poster=[]
    for i in movie_list:
        # for print title of movie
        movie_id=movies.iloc[i[0]].id
        #for fetch poster from api
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_movie_poster.append(fetch_poster(movie_id))
    return recommend_movie,recommend_movie_poster


movie_dict=pickle.load(open('movies_dict.pickle','rb'))
movies=pd.DataFrame(movie_dict)

similarity=pickle.load(open('similarity.pickle','rb'))

st.title("Movie Recommendation System")
select_movie=st.selectbox('How Would you like to be contracted ?',
             movies['title'].values)

if st.button("Recommend Movie"):

    name,poster=recommend(select_movie)
    st.balloons()

    st.subheader("wait for execution")
    with st.spinner("wait for it-----"):
        time.sleep(2)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    
    with col4:
        st.text(name[3])
        st.image(poster[3])
    
    
    with col5:
        st.text(name[4])
        st.image(poster[4])
    



 


