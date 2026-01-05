<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Mau</title>
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="flex flex-col p-5 gap-4 min-h-screen mx-auto max-w-5xl">
        @if($selected)
            <div class="flex flex-col justify-center items-center gap-4">
                <img src="data:image/jpeg;base64,{{ $selected['base64'] }}" class="max-w-sm rounded-lg" />
                <h2 class="text-xl font-semibold">{{ $selected["name"] }}</h2>
            </div>
        @endif
        <div class="grid grid-cols-4 gap-5">
            @foreach($images as $image)
                <div class="relative group">
                    <img
                        src="data:image/jpeg;base64,{{ $image['base64'] }}"
                        class="w-full rounded-lg border-2 border-transparent hover:border-blue-500 transition-all"
                    />
                    <form method="GET" action="/" class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <input type="hidden" name="selected" value="{{ $image['name'] }}" />
                        <button type="submit" class="bg-blue-500 text-white px-3 py-1 rounded-md">
                            Select
                        </button>
                    </form>
                </div>
            @endforeach
        </div>
    </body>
</html>
