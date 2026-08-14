# Solution Guide

The comments template renders `row.body|safe`, which disables normal escaping and allows stored script-like content to be interpreted by the browser.

Evidence:

- submitted comment body
- rendered comments page
- `web.xss.pattern` event in the logging API

Fix: remove `|safe`, encode output by context, validate input where appropriate, and add content security controls.

