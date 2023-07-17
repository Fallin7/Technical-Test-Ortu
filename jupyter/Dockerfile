FROM jupyter/base-notebook:latest

# install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["jupyter", "notebook", "--no-browser","--NotebookApp.token=''","--NotebookApp.password=''"]

