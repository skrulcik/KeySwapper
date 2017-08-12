# KeySwapper

Swaps secret keys with a text placeholder for safe publishing.

## Motivation

Usually, code that requires using a private key or client secret is published
with a placeholder. This utility makes it easy to swap secret keys with
placeholders and visa versa.

## Usage

### Adding Placeholders in Your Code

Wherever you *would* put a secret key, put a placeholder instead.

```swift
let CLIENT_SECRET = "CLIENT_SECRET_PLACEHOLDER"
let PRIVATE_KEY = "PRIVATE_KEY_PLACEHOLDER"
```

### Store Secret Keys

Put your keys in a folder that will *not* be added to your git repo. The
following commands are one way to create such a folder, but not the only way.

```bash
# From the root of your git repo
mkdir .keys
echo '.keys' >> .gitignore
git add .gitignore
git commit -m 'Add key directory to gitignore'
```

Then, create a file inside the key directory for each secret key. The name of
the file should be the name of the placeholder you use in your code, and the
contents of the file will be the contents of the key (this is why it is
important not to track this directory with your VCS).

```bash
# If your keys are in environment variables
cat $CLIENT_SECRET > .keys/CLIENT_SECRET_PLACEHOLDER
cat $PRIVATE_KEY > .keys/PRIVATE_KEY_PLACEHOLDER
```

It is also common to copy a key from online. If you're using a mac, you can
paste into your secret file like so:

```bash
pbpaste > .keys/CLIENT_SECRET_PLACEHOLDER
```

### Conceal or Reveal Secret Keys

Now that you have placeholders in your code, and secret keys in your key
directory, you can hide or show the keys whenever you want.

To "reveal" the keys in your code, run the following:

```bash
./keyswapper.py --reveal # -r for short
```

To "conceal" the keys in your code, which you MUST do before committing any
changes, run the following:

```bash
./keyswapper.py --conceal # -c for short
```

Both of the above commands assume you put your keys in a directory named
`.keys` and you want to swap keys in the current directory and its
subdirectories. These assumptions can be changed using the `--keydir` and
`--path` options, respectively. See `./keyswap.py --help` for the full list of
command line args.

### Usage Example

First, clone this repository and navigate to the example directory.

```bash
git clone git@github.com:skrulcik/KeySwapper
cd KeySwapper/example
```

The contents of testFile should be:

```
What does the PLACEHOLDER1 look like replaced?
What does the PLACEHOLDER2 look like replaced?
```

After running `../keyswap.py -r`, the contents should be:

```
What does the ThisIsKey1 look like replaced?
What does the ThisIsKey2 look like replaced?
```

After running `../keyswap.py -r`, the contents should return to:

```
What does the PLACEHOLDER1 look like replaced?
What does the PLACEHOLDER2 look like replaced?
```

