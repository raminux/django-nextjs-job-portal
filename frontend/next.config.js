/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    API_URL: "http://localhost:8000",
    MAPBOX_ACCESS_TOKEN: 'pk.eyJ1IjoicmFlcyIsImEiOiJjbDl0MzRhaGsxczB2M29uc3ZzZXN1ZzZkIn0.xyam4b5hPITh_uoCts0CXQ', 
  }
}

module.exports = nextConfig
