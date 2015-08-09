/* Module */
var express = require('express');


var app = express();
app.use(express.static('public'));

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    //var err = new Error('Not Found');
    //err.status = 404;
    //next(err);
    console.log(req.path);
    res.status(404).json({
    	messages: "404 Not Found"
    });
});


module.exports = app;
