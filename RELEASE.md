# Release sphinxcontrib-httpdomain

Use uv and make to release sphinxcontrib-httpdomain.

Check the current version.

```shell
uv version
```

Find the correct command to bump the version from [uv's documentation](https://docs.astral.sh/uv/guides/package/#updating-your-version).
Use `--dry-run` to check that the command will do what you expect.

```shell
uv bump --dry-run <args>
```

If it looks good, then drop the `--dry-run` flag, and run the command.

```shell
uv bump <args>
```

Commit the changes, tag the commit, push to the repository, clean the `dist` directory, build the project.

```shell
make dist
```

Publish the project.
You'll need your personal access token from PyPI.

```shell
uv publish --username __token__
```

Finally, navigate to the [New release page](https://github.com/sphinx-contrib/httpdomain/releases/new) on GitHub to publish the tagged release.
