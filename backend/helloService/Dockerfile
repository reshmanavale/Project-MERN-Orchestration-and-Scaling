FROM node:18
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Set environment variable directly in Dockerfile
ENV PORT=3001

EXPOSE 3001

CMD ["node", "index.js"]

