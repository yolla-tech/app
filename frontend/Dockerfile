# Use the official Node.js Alpine image for a smaller build size
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json first (for better caching)
COPY package.json package-lock.json ./

# Install dependencies (omit dev dependencies for smaller image size)
RUN npm ci --omit=dev

# Copy the rest of the app's code
COPY . .

# Build the React app
RUN npm run build

# Install 'serve' to serve the production build
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Serve the built app using 'serve'
CMD ["serve", "-s", "build", "-l", "3000"]
