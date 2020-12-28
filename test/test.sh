#! /bin/bash

TEST_INPUT="test_input.ts"
TEST_OUTPUT="test_output.ts"
OUTPUT="output.ts"

cat > $TEST_INPUT <<-EOM
function foo() {
    function bar() {
        function baz() {

        }
    }
}

function * foo() {
    function * bar() {
        function * baz() {

        }
    }
}
EOM

cat > $TEST_OUTPUT <<-EOM
function
foo()
{
    function
    bar()
    {
        function
        baz()
        {

        }
    }
}

function *
foo()
{
    function *
    bar()
    {
        function *
        baz()
        {

        }
    }
}
EOM

fmt-ts $TEST_INPUT > "output.ts"

if cmp --silent "$TEST_OUTPUT" "$OUTPUT"; then
    exit 0
else
    diff $TEST_OUTPUT $OUTPUT -y
fi