<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{{ config('app.name', 'Laravel') }}</title>
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="flex flex-col p-5 justify-center items-center min-h-screen">
        <div class="grid grid-cols-3 gap-5">
            @foreach($images as $image)
                <img src="data:image/[image-type];base64,{{ $image }}" />
            @endforeach
        </div>
    </body>
</html>
