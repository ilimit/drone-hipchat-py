FROM python:2.7.15-onbuild
ADD notify.py /bin/
ENTRYPOINT /bin/notify.py
