# syntax=docker/dockerfile:1
# check=error=true

# Builder stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

# Test stage
FROM node:18-alpine AS tester
WORKDIR /app
COPY --from=builder /app .
CMD ["npm", "test"]

# Production stage
FROM nginx:alpine AS production
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]