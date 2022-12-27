# 情書（Love Letter）
![image](https://b.ecimg.tw/items/DEAM6UA9007S972/000001_1483519203.jpg)

# 程式語言與框架
- 前端(代定): Vue、React
- 後端: Python(FastAPI)
- MongoDB

# Practice Stack
- 三層式架構 (MVC）
- 用 event storming，找出遊戲的功能與流程
- 用 example mapping，確定需求的具體內容
- Test-Driven Development: ATDD
- DevOps: CI/CD Pipeline
- OOAD

# Other
- Github flow(Issue、Pull requests、Projects)

# 期望推進的方向
- 因為我對上面的一些Practice stack也不太熟悉，所以希望會是大家一起討論出自己覺得對的方式，藉此來一起踩雷、學習XD
- 大家一起做code review

# 環境建置
### Poetry
  ```shell
  # install with poetry.lock
  poetry install
  ```
### pre-commit
  ```shell
  # 將 pre-commit hook 安裝至專案裡的 .git/hooks 資料夾底下
  pre-commit install --install-hooks
  
  # 執行git commit的時候就會觸發到.pre-commit-config.yaml了
  ```

# 教學文
- [Poetry](https://blog.kyomind.tw/python-poetry/)
  - ```
    poetry init  # 初始化，建立pyproject.toml
    poetry env use python  # 建立專案虛擬環境並使用
    poetry shell  # 啟用虛擬環境，若沒有虛擬環境自動幫你建立並使用
    poetry install  # 依poetry.lock記載的套件版本安裝到虛擬環境中，類似npm install \
    poetry add xxx  # == pip install xxx
    poetry remove xxx  # == pip uninstall xxx
    
    # 將現有的requirements.txt轉成poetry
    cat requirements.txt | xargs poetry add
    
    # 輸出 Poetry 虛擬環境的 requirements.txt
    poetry export -f requirements.txt -o requirements.txt --without-hashes 
    ```
- [Black官方整合Pycharm](https://black.readthedocs.io/en/stable/integrations/editors.html)