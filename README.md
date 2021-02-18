# hangman

hangman is a RPC API for hosting simple hangman games. You could play in Postman, your browser, or build your own client to consume the hangman API.

You can also clone this repo and host your own server.

## Endpoints

### /api/start

This endpoint begins a new game and returns a game ID. The game ID is a 5 length string which serves as a unique identifier for each game.

This endpoint accepts `POST` requests only.

#### Request

```sh
Header          Value
Content-Type    application/json
```

```sh
Body
{
    "difficulty": "E"
}
```

`"difficulty"` can be assigned any one of `"E"`, `"M"`, and `"H"` for Easy, Medium, and Hard respectively.

#### Response

##### 200 OK

A `200 OK` response is recieved when the request difficulty is a valid option.

```sh
{
    "id": "erkL7"
}
```

##### 400 BAD REQUEST

A request with an invalid option for difficulty or no difficulty field at all recieves a response of `400 BAD REQUEST`.

```sh
{
    "difficulty": "Please provide a value for difficulty"
}

OR

{
    "difficulty": "Invalid value set for difficulty. E - Easy, M - Medium, H - Hard"
}
```

### /api/state

This endpoint gives the current state of a game.

This endpoint accepts `POST` requests only.

#### Request

```sh
Header          Value
Content-Type    application/json
```

```sh
Body
{
    "id": "erkL7"
}
```

`"id"` should be assigned the game ID value gotten when a new game is started.

#### Response

##### 200 OK

A `200 OK` response is recieved when a game with the given ID exists.

```sh
{
    "id": "erkL7",
    "difficulty": "E",
    "missed_letters": "",
    "correct_letters": "",
    "max_guesses": 8,
    "board": "______",
    "secret_set": "Animals",
    "is_done": false,
    "result": ""
}
```

There is a `"secret_word"` field which is ommitted from responses when the game is not over `(is_done = false)`. If the game is over, `"is_done"` is set to `true`, `"result"` is set to `"W"` or `"L"` to signify Win or Lose, and the secret word is provided in the response.

##### 400 BAD REQUEST

A request with no id field recieves a response of `400 BAD REQUEST`

```sh
{
    "id": "Please provide a value for id"
}
```

##### 404 NOT FOUND

A request with an invalid option for id recieves a response of `404 NOT FOUND`

```sh
{
    "id": "Game with provided id does not exist"
}
```

### /api/guess

This endpoint takes a guess and checks if it is correct, registers a correct letter or missed letter, and checks if the game is won or lost. It returns an identical response body as `/api/state` does, except it carries out a state transition before returning a response.

This endpoint accepts `POST` requests only.

#### Request

```sh
Header          Value
Content-Type    application/json
```

```sh
Body
{
    "id": "erkL7",
    "guess": "a"
}
```

`"id"` should be assigned the game ID value gotten when a new game is started. `"guess"` should be assigned a single letter.

#### Response

##### 200 OK

A `200 OK` response is recieved when a game with the given ID exists, and a valid guess is supplied.

```sh
{
    "id": "erkL7",
    "difficulty": "E",
    "missed_letters": "",
    "correct_letters": "a",
    "max_guesses": 8,
    "board": "_a____",
    "secret_set": "Animals",
    "is_done": false,
    "result": ""
}
```

##### 400 BAD REQUEST

A request with no id field and/or no guess field recieves a response of `400 BAD REQUEST`.

```sh
{
    "id": "Please provide a value for id",
    "guess": "Please provide a value for guess"
}
```

A request with an invalid option for guess recieves a response of `400 BAD REQUEST`.

```sh
{
    "guess": "Please enter a single letter"
}

OR

{
    "guess": "You have already guessed that letter"
}

OR

{
    "guess": "Please enter a LETTER"
}
```

A request to the `/api/guess` endpoint when the game is over recieves a response of `400 BAD REQUEST`.

```sh
{
    "message": "Game is over"
}
```

##### 404 NOT FOUND

A request with an invalid option for id recieves a response of `404 NOT FOUND`.

```sh
{
    "id": "Game with provided id does not exist"
}
```

## Hosting your own server

Clone the `hangman` repo.

```sh
git clone https://github.com/ahira-justice/hangman.git
```

In `.gitlab-ci.yml` and `app/settings.py`, there is a default configuration for a heroku deployment. Leave `Procfile` and `runtime.txt` as is.

Set a gitlab remote repo,

```sh
git remote add ciorigin https://gitlab.com/example/hangman.git
```

In your gitlab CI/CD settings, configure three environment variables, `SECRET_KEY`, `APP_NAME`, and `HEROKU_STAGING_API_KEY`.

In your heroku app settings, configure `SECRET_KEY` and `SITE_URL`.

Push to `ciorigin`,

```sh
git push ciorigin
```

The CI/CD workflow will deploy to your heroku app after passing the `test` stage.

If you want to deploy to your own VPS or a different cloud platform, modify `.gitlab-ci.yml` and/or `app/settings` as you see fit.

## Dependencies

A full list of dependencies is found in `requirements.txt`

## License

[GNU GENERAL PUBLIC LICENSE](LICENSE)
