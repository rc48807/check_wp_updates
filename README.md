# check_wp_updates
Monitoring of WordPress updates. 

WordPress is a Content management tool (CMS) designed to facilitate the creation and robust administration of websites, blogs or applications, ensuring usability and aesthetics, which is why one of the CMS with the largest market share.
It is a software in constant development, and as such susceptible to application or project vulnerabilities, which are frequently corrected by security versions, available in its official site on the Internet. However, the discovery of new updates is not always a trivial process, which causes many users to use for wide-time versions of outdated and publicly known vulnerabilities.

This Nagios plugin monitors the version of WordPress, in search of updates, receiving as an argument the full path of the version.php file, where you get information about the version of the software installed, and uses WordPress's Web service to obtain the latest version available at the official site of WordPress, by conversing and notifying the critical state whenever new version or update is detected.

Mandatory arguments: The following argument must be specified when the module is executed:

-p or --path used to specify the full path to the version.php file.

Optional arguments: The following arguments are optionally invoked, as user needs:

-V or --version used to query the module version.

-A or --author used to query the author's data.

Command-Line Execution Example:

./check_wp_update.py -p /var/www/html/wp-includes/version.php

