FROM node:18
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Set environment variables directly
ENV PORT=3002
ENV MONGO_URL=mongodb://<mongo-host>:27017/profiledb

EXPOSE 3002

CMD ["node", "index.js"]
