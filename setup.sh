mkdir -p ~/.streamlit/


echo  "\
[sever]\n\
port= $PORT\n\
enableCORS= false\n\
headless= true\n\
\n\
" > ~/.streamlit/config.toml
