# Octopus Deploy plugin


[![Build Status][xlr-samson-plugin-travis-image]][xlr-samson-plugin-travis-url]
[![Maintainability][xlr-samson-plugin-Maintainability-url]][xlr-samson-plugin-Maintainability-image]
[![Codacy Badge][xlr-samson-plugin-Codacy-url]][xlr-samson-plugin-Codacy-image]
[![License: MIT][xlr-samson-plugin-license-image]][xlr-samson-plugin-license-url]
![Github All Releases][xlr-samson-plugin-downloads-image]

[xlr-samson-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-samson-plugin.svg?branch=master
[xlr-samson-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-samson-plugin
[xlr-samson-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-samson-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-samson-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-samson-plugin/total.svg
[xlr-samson-plugin-Maintainability-url]: https://api.codeclimate.com/v1/badges/ca5d70a7bbb5d238bfdf/maintainability
[xlr-samson-plugin-Maintainability-image]: https://codeclimate.com/github/xebialabs-community/xlr-samson-plugin/maintainability
[xlr-samson-plugin-Codacy-url]: https://api.codacy.com/project/badge/Grade/ff2717a153b64ca096313015ca7207f7
[xlr-samson-plugin-Codacy-image]: https://www.codacy.com/app/Rick-BrokerOrganization/xlr-samson-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-samson-plugin&amp;utm_campaign=Badge_Grade

## Preface

This document describes the functionality provided by the XL Release Samson plugin.

See the [XL Release reference manual](https://docs.xebialabs.com/xl-release) for background information on XL Release and release orchestration concepts.  

## Overview

This XL Release plugin can trigger deployments on Samson.

## Requirements

* XL Release 7.0+

## Installation

* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xlr-samson-plugin/releases) into the `XL_RELEASE_SERVER/plugins` directory or use the Plugin Manager.
* Restart the XL Release server.

## Usage

### Deploy

Deploy to stages based on Commit SHA, Webhook ID and giving a message.