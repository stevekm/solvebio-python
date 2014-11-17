# -*- coding: utf-8 -*-
import solvebio

from netrc import netrc as _netrc, NetrcParseError
from urlparse import urlparse
import os


class netrc(_netrc):
    """
    Adds a save() method to netrc
    """
    @staticmethod
    def path():
        try:
            path = os.path.join(
                os.environ.get('NETRC_PATH', os.path.join(os.environ['HOME'], '.solvebio')),
                               ".netrc")
        except KeyError:
            raise IOError("Could not find .netrc: neither $NETRC_PATH "
                          "nor is '$HOME/.solvebio/.netrc set")

        # create an empty .netrc if it doesn't exist
        if not os.path.exists(path):
            try:
                open(path, 'a').close()
            except IOError:
                raise Exception("Could not create a netrc file at '%s', "
                                "permission denied." % path)
        return path

    def save(self, path):
        """Dump the class data in the format of a .netrc file."""
        rep = u""
        for host in self.hosts.keys():
            attrs = self.hosts[host]
            rep = rep + "machine " + host + "\n\tlogin " \
                + unicode(attrs[0]) + "\n"
            if attrs[1]:
                rep = rep + "account " + unicode(attrs[1])
            rep = rep + "\tpassword " + unicode(attrs[2]) + "\n"
        for macro in self.macros.keys():
            rep = rep + "macdef " + macro + "\n"
            for line in self.macros[macro]:
                rep = rep + line
            rep = rep + "\n"

        f = open(path, 'w')
        f.write(rep)
        f.close()


class CredentialsError(BaseException):
    """
    Raised if the credentials are not found.
    """
    pass


def get_credentials():
    """
    Returns the tuple user / password given a path for the .netrc file.
    Raises CredentialsError if no valid netrc file is found.
    """
    try:
        netrc_path = netrc.path()
        auths = netrc(netrc_path).authenticators(
            urlparse(solvebio.api_host).netloc)
    except (IOError, TypeError, NetrcParseError) as e:
        raise CredentialsError(
            'Could not open .netrc file: ' + str(e))

    if auths:
        return (auths[0], auths[2])
    else:
        return None


def delete_credentials():
    try:
        netrc_path = netrc.path()
        rc = netrc(netrc_path)
    except (IOError, TypeError, NetrcParseError) as e:
        raise CredentialsError('Could not open netrc file: ' + str(e))

    try:
        del rc.hosts[urlparse(solvebio.api_host).netloc]
    except KeyError:
        pass
    else:
        rc.save(netrc_path)


def save_credentials(email, api_key):
    try:
        netrc_path = netrc.path()
        rc = netrc(netrc_path)
    except (IOError, TypeError, NetrcParseError) as e:
        raise CredentialsError('Could not open netrc file: ' + str(e))

    # Overwrites any existing credentials
    rc.hosts[urlparse(solvebio.api_host).netloc] = (email, None, api_key)
    rc.save(netrc_path)
