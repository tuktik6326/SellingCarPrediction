FROM python:3.11.4-bookworm

WORKDIR /root/code


RUN pip3 install --upgrade pip
RUN pip3 install ipykernel
RUN pip3 install scikit-learn
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install ppscore
RUN pip3 install seaborn
RUN pip3 install XGBoost
RUN pip3 install dash
RUN pip3 install dash_bootstrap_components

CMD tail -f /dev/null