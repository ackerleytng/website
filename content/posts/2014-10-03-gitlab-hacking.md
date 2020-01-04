---
slug: gitlab-hacking
date: "2014-10-03T00:00:00Z"
description: GitLab Hacking
tags:
- gitlab
- hacking
- ruby
- rails
title: GitLab Hacking
---
## To disable minifying of the js file, comment this line out

    user@ubuntu:/opt/gitlab/embedded$ sudo vim ./service/gitlab-rails/config/environments/production.rb
    #config.assets.js_compressor = :uglifier

## gitlab-rake is a script that sets a default user and does bundle exec rake

Needs permission to write, so change permissions for public folder

    sudo chmod a+w public
    cd public
    sudo chmod a+w assets

## To recompile fully

    sudo gitlab-rake assets:clobber --trace # this step is sort of optional if you don't want to completely clean it out
    sudo gitlab-rake assets:precompile --trace
    sudo gitlab-ctl restart

## Add all accepted mimetypes to this file

    /opt/gitlab/embedded$ sudo vim service/gitlab-rails/app/javascripts/markdown_area.js.coffee
    acceptedFiles: "image/*,audio/*,video/*,application/*,text/*"

## Disable checking of extensions

    /opt/gitlab/embedded$ sudo vim service/gitlab-rails/app/services/projects/image_service.rb

Replace

    if image && correct_mime_type?(image)

with

    if image

## Change the function formatLink

    /opt/gitlab/embedded$ sudo vim service/gitlab-rails/app/javascripts/markdown_area.js.coffee
  
    String::endsWith = (s) -> s is '' or @[-s.length..] is s
  
    formatLink = (str) ->
      image_extensions = ['jpg', 'gif', 'jpeg', 'png']
  
      is_image = false
      for ext in image_extensions
        is_image = is_image | str.url.toLowerCase().endsWith(ext)
  
      if is_image
        "![" + str.alt + "](" + str.url + ")"
      else
        "[" + str.alt + "](" + str.url + ")"
  
## Changing html in views (changing the text)

Go to /opt/gitlab/embedded/service/gitlab-rails/app/views/projects/wikis
Modify the .haml files.
Restart server to see effects

Replace 

    .pull-right Attach images (JPG, PNG, GIF) by dragging & dropping or #{link_to "selecting them", '#', class: 'markdown-selector' }.

with

    .pull-right Attach files by dragging & dropping.

## Change maximum filesize for uploads

    /opt/gitlab/embedded$ sudo vim service/gitlab-rails/app/javascripts/markdown_area.js.coffee

Change line 29. The unit of memory for that value is MiB.

## Remove dropzone's check

    /opt/gitlab/embedded$ sudo vim service/gem/ruby/2.1.0/gems/dropzonejs-rails-0.4.14/vendor/javascripts/dropzone.js

    } else if (!Dropzone.isValidFile(file, this.options.acceptedFiles)) {
      return done(this.options.dictInvalidFileType);

## Clear out accepted_images

I think this makes the FileUploader class not check extensions

    /opt/gitlab/embedded$ sudo vim service/gitlab-rails/app/services/projects/image_service.rb

Make accepted_images return nothing

    def accepted_images
      #%w(png jpg jpeg gif pdf zip tar.gz txt)
    end
