# Minitest Buddy

A small Sublime Text package to boost your productivity when using Minitest.

## Features

- provides command and shortcut for toggling between implementation/test files

## Bindings

The default binding for toggling is `super+;`
```json
{
  "keys": ["super+;"],
  "command": "minitest_toggle"
}
```

You can change it to whatever you want by adding the following snippet to your Keybindings file.
```json
{
  "keys": ["ctrl+alt+down"],
  "command": "minitest_toggle"
}
```

## Installation

This plugin is not available on package control yet as [my PR](https://github.com/wbond/package_control_channel/pull/7790) is waiting for review.

You can install it by cloning this repo in your `Packages` directory.

## How it works

```
project/
  - foo.rb
  test/
    - test_foo.rb
```

Once the toggle command is hit this package will figure whether or not the current file is a test or a implementation file. This is done by checking if the file name starts with `test_`.

### Current file is a implementation file

If it is a implementation file (`foo.rb`), the package will look for any `test_foo.rb` inside the `test` directory.

### Current file is a test file

If it is a test file (`test_foo.rb`), the package will look for any `foo.rb` inside the `project` directory.

### Multiple files found

If more than one file is found, a quick panel will appear so you can choose the one you want to open.

## Similar packages

- [RSpec Buddy](https://github.com/glaucocustodio/rspec-buddy-for-sublime-text)

## License

The gem is available as open source under the terms of the MIT License.
