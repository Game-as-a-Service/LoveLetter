FROM node:16-alpine AS deps
WORKDIR /app

COPY frontend/package.json ./
RUN yarn

FROM node:16-alpine AS frontend-builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY frontend .
RUN yarn build

FROM python:3.10 AS runner
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && pip install poetry && poetry update

COPY --from=frontend-builder /app/build ./static_files
COPY love_letter ./love_letter
ENV static_files=/app/static_files
CMD poetry run uvicorn love_letter.web.app:app --host 0.0.0.0 --port 5566


