# 情書（Love Letter）

![image](https://b.ecimg.tw/items/DEAM6UA9007S972/000001_1483519203.jpg)

## 專案架構

### 技術框架

- 前端: React
- 後端: Python(FastAPI)
- MongoDB

### Practice Stack

- 三層式架構 (MVC）=> clean architecture(CA)
- 用 event storming，找出遊戲的功能與流程
- 用 example mapping，確定需求的具體內容
- Test-Driven Development: ATDD
- DevOps: CI/CD Pipeline
- OOAD

## 環境建置

### Python server

我們使用 [Poetry](https://python-poetry.org/docs/) 管理dependencies與虛擬環境。
安裝Poetry之後，在專案根目錄執行以下指令：

```shell
# Activate the virtual env.
poetry shell
# Install dependencies into the virtual env.
poetry install
# Run the Python server
poetry run app

```

用瀏覽器開啟 [http://localhost:8080/docs](http://localhost:8080/docs)，可以看到後端的Swagger API docs。

### Front-end server

確定本機已安裝 [NodeJS](https://nodejs.org/en/download/)。開啟一個新的Terminal，在專案根目錄執行以下指令：

```shell
# Enter the folder /frontend
cd frontend/
# Install dependencies
npm i
# Run the React app
npm start
```

前端 React app 將運行於本機 [http://localhost:3000/](http://localhost:3000/)。

## 協作開發

### Code Style and Formatting

使用 [pre-commit](https://pre-commit.com/) 來確認你commit的程式碼有一致的格式。
在安裝 `pre-commit` 之後，在專案根目錄執行以下指令：

```shell
# 將 pre-commit hook 安裝至專案裡的 .git/hooks 資料夾底下
pre-commit install --install-hooks

```

此後，在專案執行 `git commit` 時， `pre-commit` 將會依照 `.pre-commit-config.yaml` 內的設定將你新增或修改的程式碼格式化。

### 測試

執行單元測試(unit tests)

```shell
poetry run pytest
```

執行行為測試

```shell
poetry run behave
```

執行CI的測試

```shell
./tests/run-tests.sh
```

## 參考

- [Poetry](https://blog.kyomind.tw/python-poetry/)

```shell
poetry init  # 初始化，建立 pyproject.toml
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

- [整合Black進Pycharm](https://black.readthedocs.io/en/stable/integrations/editors.html)

