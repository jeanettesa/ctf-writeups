# Beginner's Web
A simple web app with back end logic coded in JavaScript/fastify. \
The front end lets you enter a string which can be converted to base64 or scrypt
before output.

## Problem:
How can we output the flag variable which is stored
inside the JavaScript code that runs on the web app backend?

## Web app code shared for the challenge:

### app.js
```
const fastify = require('fastify');
const nunjucks = require('nunjucks');
const crypto = require('crypto');


const converters = {};

const flagConverter = (input, callback) => {
  const flag = '*** CENSORED ***';
  callback(null, flag);
};

const base64Converter = (input, callback) => {
  try {
    const result = Buffer.from(input).toString('base64');
    callback(null, result)
  } catch (error) {
    callback(error);
  }
};

const scryptConverter = (input, callback) => {
  crypto.scrypt(input, 'I like sugar', 64, (error, key) => {
    if (error) {
      callback(error);
    } else {
      callback(null, key.toString('hex'));
    }
  });
};


const app = fastify();
app.register(require('point-of-view'), {engine: {nunjucks}});
app.register(require('fastify-formbody'));
app.register(require('fastify-cookie'));
app.register(require('fastify-session'), {secret: Math.random().toString(2), cookie: {secure: false}});

app.get('/', async (request, reply) => {
  reply.view('index.html', {sessionId: request.session.sessionId});
});

app.post('/', async (request, reply) => {
  if (request.body.converter.match(/[FLAG]/)) {
    throw new Error("Don't be evil :)");
  }

  if (request.body.input.length < 20) {
    throw new Error('Too short :(');
  }

  if (request.body.input.length > 1000) {
    throw new Error('Too long :(');
  }

  converters['base64'] = base64Converter;
  converters['scrypt'] = scryptConverter;
  converters[`FLAG_${request.session.sessionId}`] = flagConverter;

  const result = await new Promise((resolve, reject) => {
    converters[request.body.converter](request.body.input, (error, result) => {
      if (error) {
        reject(error);
      } else {
        resolve(result);
      }
    });
  });

  reply.view('index.html', {
    input: request.body.input,
    result,
    sessionId: request.session.sessionId,
  });
});

app.setErrorHandler((error, request, reply) => {
  reply.view('index.html', {error, sessionId: request.session.sessionId});
});

app.listen(59101, '0.0.0.0');
```

### index.html ###
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.0/milligram.css">
    <title>Beginner's Web: OmniConverter</title>
    <style>
      body {
        text-align: center;
      }
      .row {
        justify-content: center;
        margin: 1rem 0 1.5rem;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>OmniConverter</h1>
      {% if error %}
        <h2>ERROR: {{error}}</h2>
      {% endif %}
      <form method="POST">
        <textarea name="input" minlength="20">{{input}}</textarea>
        <div class="row">
          <select class="column column-20" name="converter">
            <option value="base64">Base64</option>
            <option value="scrypt">scrypt</option>
          </select>
          <button class="column column-10" type="submit">Convert</button>
        </div>
        <textarea disabled>{{result}}</textarea>
      </form>
      <p>Session ID: {{sessionId}}</p>
    </div>
  </body>
</html>
```

## What data can be posted to the back end of this web app?
* input *(request.body.input)*
* converter *(request.body.converter)*

## Where is the flag stored?
The flag is stored within the flagConverter function:
```
const flagConverter = (input, callback) => {
  const flag = '*** CENSORED ***';
  callback(null, flag);
};
```

Every time we post new data to the web app, the flagConverter function gets
assigned to the *converters* object, \
with the key: *FLAG_${request.session.sessionId}*.\
Code:
``  converters[`FLAG_${request.session.sessionId}`] = flagConverter;``

## How is this web app vulnerable?
The *converters* object can be manipulated by our inputs, as shown in the code:
```
const result = await new Promise((resolve, reject) => {
  converters[request.body.converter](request.body.input, (error, result) => {
    if (error) {
      reject(error);
    } else {
      resolve(result);
    }
  });
});
```

### First thoughts on how to get the flag ###
If it was possible, we would give as input that the converter (request.body.converter)
is 'FLAG_${request.session.sessionId}', with request.body.input set to any
arbitrary string between 20 and 1000 characters (to avoid the web app throwing
an error).

Then the resulting code (depending on the sessionId, with example input
'zzzzzzzzzzzzzzzzzzzz') would be something like:
```
const result = await new Promise((resolve, reject) => {
  converters['FLAG_R3EJRIyxaosT3czNb-qxApiZuWbYTRQH']('zzzzzzzzzzzzzzzzzzzz', (error, result) => {
    if (error) {
      reject(error);
    } else {
      resolve(result);
    }
  });
});
```

Meaning, more specifically, we would call the flagConverter function in the
following way:
```
const result = await new Promise((resolve, reject) => {
  flagConverter('zzzzzzzzzzzzzzzzzzzz', (error, result) => {
    if (error) {
      reject(error);
    } else {
      resolve(result);
    }
  });
});
```

Provided the Promise resolved successfully, this would give us the flag.

However, since the converter variable can not match the /[FLAG]/ regex, we will be
unsuccessful setting the converter (request.body.converter) to
'FLAG_${request.session.sessionId}''.
