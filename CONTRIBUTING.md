# Contributing to Cellenics
Thank you for your interest in contributing to Cellenics! We welcome all people who want to contribute in a healthy and constructive manner within our community. To help us create a safe and positive community experience for all, we require all participants to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).


## Where to start
1. Choosing what to work on.

A good place to start is our [Trello board with user requests](https://trello.com/b/zPaytPFR/usability-studies). In there, we log all issues, reported by our users as well as their feature requests and we let them vote on what is most important. Pick a task, assign it to yourself and move it to "in progress" column. If you have any questions and for a technical chat about what is the best approach, message iva@biomage.net or marcell@biomage.net.

2. Fix a bug or improve existing docs.

Make a new card for this in our board: [Trello board with user requests](https://trello.com/b/zPaytPFR/usability-studies). Add @ivababukova from the core development team to the card. Assign it to yourself and move it to "in progress" column.

3. Have an idea about an awesome new feature that is not on the board yet.

How exciting, we want to hear more! Create a new card for this in our board: [Trello board with user requests](https://trello.com/b/zPaytPFR/usability-studies) and add @ vickymorrison who is our product owner. She will chat with you more and help you make wireframes if applicable. 

## Definition of D.O.N.E.

In order for a change to be considered as done, it has to comply with all of the items below:
1. The changes are tested end to end using [inframock](https://github.com/biomage-ltd/inframock). Everything works as expected and the changes implement all requirements listed in the issue. 
2. Code passes existing unit tests and CI checks.
3. There are unit tests added to test the new functionality.
4. Where relevant, operational and developer documentation is updated.
5. All the code is peer reviewed and approved by at least one member of the core development team (currently marcellp or ivababukova).
6. If the feature entails change of UX, the change is reviewed and approved by Vicky Morrison (vickymorrison) before releasing to production.

## Raising a Pull Request
Your change works and complies with the points [1-4] from the definition of Done? If that is the case is time for a pull request! When raising a PR, make sure that:
1. Follow the auto-generated instructions on your PR description - add all necessary information, complete all compulsory actions.
2. Assign the PR to a member of the core development team who will review your change.

## Development Environment
The following versions of runtime and programming languages are currently used on our development (as of 10 Dec 2021) : 

- Python 3.8 - [worker](https://github.com/biomage-ltd/worker)
- R 4.0.5 - [worker](https://github.com/biomage-ltd/worker) and [pipeline](https://github.com/biomage-ltd/pipeline)
- Node 14.18.1 - [API](https://github.com/biomage-ltd/api) and [UI](https://github.com/biomage-ltd/ui)

Popular questions
-----------------
* __How do I stage an environment?__ Very easy! We have a command for that. It is all explained in the [biomage-utils](https://github.com/biomage-ltd/biomage-utils) repository.
* __How do I make infrastructure changes?__ We have an [infrastructure directory](https://github.com/biomage-ltd/developer-docs/blob/master/INFRASTRUCTURE.md#directory) in place to find where to find and how to edit configuration files related to infrastructure
* __I have trouble running a particular application in this organization, what do I do?__ Talk to us, we would love to help! You can reach us on engineering@biomage.net. We will reply as soon as we can :)
