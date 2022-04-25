package todoapp

import (
	"dagger.io/dagger"
	"dagger.io/dagger/core"
	"universe.dagger.io/alpine"
	"universe.dagger.io/bash"
	"universe.dagger.io/docker"
	// "universe.dagger.io/netlify"
)

dagger.#Plan & {
	// _nodeModulesMount: "/src/node_modules": {
	// 	dest:     "/src/node_modules"
	// 	type:     "cache"
	// 	contents: core.#CacheDir & {
	// 		id: "todoapp-modules-cache"
	// 	}

	// }
	client: {
		filesystem: {
			"./": read: {
				contents: dagger.#FS
				exclude: [
					"shctx.cue",
				]
			}
			"./_build": write: contents: actions.build.contents.output
		}
		env: {
			APP_NAME:      string
			NETLIFY_TEAM:  string
			NETLIFY_TOKEN: dagger.#Secret
            POETRY_CACHE_DIR: string
		}
	}

	actions: {
		deps: docker.#Build & {
			steps: [
				alpine.#Build & {
					packages: {
						bash: {}
						curl: {}
						python3: {}
                        "py3-pip": {}
                        "gcc": {}
					}
				},
                docker.#Run & {
                    command: {
                        name: "bash"
                        args: ["curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -"]
                        flags: { "-c": true }
                    }
                },
                docker.#Run & {
                    command: {
                        name: "ln"
                        args: ["/root/.poetry/bin/poetry", "/usr/bin/poetry"]
                        flags: { "-s": true }
                    }
                },
                // docker.#Run & {
                //     command: {
                //         name: "pip"
                //         args: ["install", "poetry"]
                //     }
                // },
				docker.#Copy & {
					contents: client.filesystem."./".read.contents
					dest:     "/src"
				},
				bash.#Run & {
					workdir: "/src"
					mounts: {
						"/cache/pypoetry": {
							dest:     client.env.POETRY_CACHE_DIR
							type:     "cache"
							contents: core.#CacheDir & {
								id: "poetry-cache"
							}
						}
						// _nodeModulesMount
					}
					script: contents: #"""
						poetry install
						"""#
				},
			]
		}

		test: bash.#Run & {
			input:   deps.output
			workdir: "/src"
			// mounts:  _nodeModulesMount
			script: contents: #"""
				poetry run pytest
				"""#
		}

		// build: {
		// 	run: bash.#Run & {
		// 		input:   test.output
		// 		// mounts:  _nodeModulesMount
		// 		workdir: "/src"
		// 		script: contents: #"""
		// 			yarn run build
		// 			"""#
		// 	}

		// 	contents: core.#Subdir & {
		// 		input: run.output.rootfs
		// 		path:  "/src/build"
		// 	}
		// }

		// deploy: netlify.#Deploy & {
		// 	contents: build.contents.output
		// 	site:     client.env.APP_NAME
		// 	token:    client.env.NETLIFY_TOKEN
		// 	team:     client.env.NETLIFY_TEAM
		// }
	}
}
