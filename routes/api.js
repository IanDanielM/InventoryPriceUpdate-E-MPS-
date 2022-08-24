const express = require('express');
const router = express.Router();
const fetch = require('node-fetch');
const Dropbox = require('dropbox').Dropbox;
const uuid = require('uuid');
const url = require('url');
const queryString = require('querystring');
const https = require('https')
const keys = require('../config/dropboxkeys')
const fs = require("fs");

const csrfToken = uuid.v4();


router.get('/grant', (req, res, next) => {

    let options = {
        hostname: 'www.dropbox.com',
        pathname: '/oauth2/authorize',
        method: 'GET',
        query: {
            client_id: keys.clientId,
            response_type: 'code',
            redirect_uri: 'http://localhost:5000/emps/dropbox/callback',
            state: csrfToken
        }
    }
    console.log(url.format(options))
    res.status(301).redirect(`https://www.dropbox.com/oauth2/authorize?client_id=${keys.clientId}&response_type=code&redirect_uri=${options.query.redirect_uri}&state=${csrfToken}`)
});


router.get('/callback',(req, res, next) => {
    if(req.query.error){
        return res.status(401).json({
            success: false,
            msg: 'Something went wrong!',
            data: res.query.error_description
        })
    }

    if(req.query.state !== csrfToken) {
        return res.status(401).json({
            success: false,
            msg: 'CSRF Token doesnt match',
            data: null
        })
    }

    let options = {
        hostname: 'api.dropboxapi.com',
        pathname: 'oauth2/token',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }

    let bodyParams = queryString.stringify({
        code: req.query.code,
        grant_type: 'authorization_code',
        redirect_uri: 'http://localhost:5000/emps/dropbox/callback',
        client_id: keys.clientId,
        client_Secret: keys.clientSecret
    })

    https.request(options, (resp) => {
        console.log(resp.statusCode)
        if(resp.statusCode !== 200) {
            return resp.statusMessage
        }
        let creds = [];

        resp.on('data', (chunk) => {
            creds.push(chunk)
            console.log(bodyParams)
            console.log(creds)
        })

        resp.on('end', () => {
            res.end(creds.toString())
        })
    }).end(bodyParams)
})


module.exports = router;