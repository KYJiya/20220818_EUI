# python 3.10.4

# https://www.sidc.be/EUI/data/

> # 실행방법  
> python -m venv .venv  
./.venv/scripts/activate  
pip install -r requirements.txt  
python main.py  

> /data/category/index.txt 파일이 존재하는 경우, 해당 파일에서 목록을 읽어 data를 downloads한다.  
따라서 웹페이지에서 새로 download를 하고 싶다면 해당 파일을 삭제하고 프로그램을 재실행하면 된다.

> secret page에 접속하고 싶은 경우
빈 파일을 생성 후 이름을 '.env'로 만든다.
내용을 채운다.
```
id="yourid"
pw="yourpassword"
```