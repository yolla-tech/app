# syntax=docker/dockerfile:1
# check=error=true

# Builder stage with Node.js
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Test stage (new)
FROM node:18-alpine AS tester
WORKDIR /app
COPY --from=builder /app .
RUN npm test  # This executes your tests

# Production stage
FROM nginx:alpine AS production
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]