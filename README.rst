Introduction
============
fourdigits.seo brings additional Publisher and Author data support and SEO overrides support in Plone 4.

- The supported platforms for Publisher are Twitter Card, Open Graph and Google Plus.
- The title and description of the login form, registration form and contact form can be overriden.
- Favicon.ico and Apple Touch icons can be set.


Site widesettings
==================
General / default:
- Include site name in title (Include the site name in the title tag)
- Site name seperator (Separator used to separate the object title and the site name in the title tag)
- Expose Publication date (Expose publication date in the head)
- Login Form Title (Title for the login form)
- Login Form Description (Description for the homepage)
- Register Form Title (Title for the registration form)
- Register Form Description (Description for the registration form)
- Contact Info Title (Title for the contact info page)
- Contact Info Description (Description for the contact info page)

Social
- Publisher information for the major social media providers: Google Plus, Twitter Card and Open Graph.
- Google+ Publisher Page
- Expose Twitter Card
- Twitter Site Account
- Expose Open Graph
- Open Graph fallback image
- Expose Open Graph Author

Icons:
- Favicon url
- Touch icon iPhone url
- Touch icon iPhone Retina url
- Touch icon iPad url
- Touch icon iPad Retina url

Indexing:
- Index Login Form
- Index Register Form
- Index Contact Info


Per object settings
===================
- Override meta title
- Override meta description
- No Index
- No Follow
- No Archive
- No Snippet


Installation
============
- Add 'fourdigits.seo' to the eggs section of your buildout.cfg.
- Install 'SEO' using the 'Add-ons' section in the Plone control panel.
- Enable the 'SEO' behaviour in the 'Dexterity Contect Types' in the Plone Control Panel.
Note: the 'Site wide settings' are available without enableing the behavior.
