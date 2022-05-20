import axios from 'axios'

const DEBUG = true
const BASE_API_URL = 'https://vds2139329.my-ihor.ru/api'
const BASE_DEBUG_URL = 'http://192.168.1.64:5000/api'

let baseURL = DEBUG ? BASE_DEBUG_URL : BASE_API_URL

const APIFetcher = axios.create({
    baseURL: baseURL,
    headers: {
        'Access-Control-Allow-Origin': '*'
    },
})

export { APIFetcher, DEBUG }