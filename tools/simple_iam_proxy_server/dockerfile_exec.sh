# This is the main entry point, i.e. process zero, of the
# Docker container.

set -euf -o pipefail # abort script on error

# Show the version immediately, which might help diagnose problems
# from console output.
echo "This is GovReady-Q simple IAM proxy server"

# Show filesystem information because the root filesystem might be
# read-only and other paths might be mounted with tmpfs and that's
# helpful to know for debugging.
echo
echo Filesystem information:
cat /proc/mounts | egrep -v "^proc|^cgroup| /proc| /dev| /sys"
echo

# Check that we're running as the 'application' user. Our Dockerfile
# specifies to run containers as that user. But cluster environments
# can override the start user and might do so to enforce running as
# a non-root user, so this process might have started up as the wrong
# user.
if [ "$(whoami)" != "application" ]; then
	echo "The container is running as the wrong UNIX user."
	id
	echo "Should be:"
	id application
	echo
fi

# # What's the address (and port, if not 80) that end users
# # will access the site at? If the HOST and PORT environment
# # variables are set (and PORT is not 80), take the values
# # from there, otherwise default to "localhost:8000".
# ADDRESS="${HOST-localhost}:${PORT-8000}"
# ADDRESS=$(echo $ADDRESS | sed s/:80$//; )

# # Write out the settings that indicate where we think the site is running at.
# echo "Starting at ${ADDRESS} with HTTPS ${HTTPS-false}."

# Start proxy server
python3.6 iam.py
