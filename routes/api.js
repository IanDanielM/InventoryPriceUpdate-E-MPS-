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
    res.status(301).redirect(`https://www.dropbox.com/oauth2/authorize?client_id=${keys.clientId}&response_type=code&redirect_uri=${options.query.redirect_uri}&state=${csrfToken}&token_access_type=offline`)
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

    const response = req.query

    console.log("response",response)

    // write to file

    fs.writeFileSync("res.txt", JSON.stringify(response))


    let bodyParams = {
        grant_type: 'authorization_code',
        client_id: keys.clientId,
        code: req.query.code,
        client_Secret: keys.clientSecret,
        redirect_uri: 'http://localhost:5000/emps/dropbox/callback',
    }


    fetch(`https://api.dropboxapi.com/oauth2/token?grant_type=${bodyParams.grant_type}&client_id=${bodyParams.client_id}&code=${bodyParams.code}&client_secret=${bodyParams.client_Secret}&redirect_uri=${bodyParams.redirect_uri}`, {
            hostname: 'api.dropboxapi.com',
            pathname: '/oauth2/token',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
    })
    .then(res => res.json())
    .then(jsonData => {
        res.json({
            success: true,
            msg: 'Great work! Enjoy your access token & refresh token',
            data: jsonData
        })
    })
    .catch(err => console.log(err))
})


module.exports = router;