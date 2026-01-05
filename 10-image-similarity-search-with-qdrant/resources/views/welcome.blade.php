<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{{ config('app.name', 'Laravel') }}</title>
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="flex flex-col p-5 gap-8 min-h-screen">
        @if($selected)
            <div class="w-full">
                <div class="flex flex-col gap-6">
                    <div class="flex flex-col gap-2">
                        <h2 class="text-xl font-semibold">Selected Image</h2>
                        <div class="flex justify-center p-4 bg-gray-100 rounded-lg">
                            <img src="data:image/jpeg;base64,{{ $selected['base64'] }}" class="max-w-sm" />
                        </div>
                    </div>
                </div>
                <hr class="my-6 border-gray-300" />
            </div>
        @endif
        <div class="flex flex-col gap-4">
            <h2 class="text-xl font-semibold">All Images</h2>
            <div class="grid grid-cols-5 gap-5">
                @foreach($images as $image)
                    <div class="relative group">
                        <img
                            src="data:image/jpeg;base64,{{ $image['base64'] }}"
                            class="w-full rounded-lg border-2 border-transparent hover:border-blue-500 transition-all"
                        />
                        <form method="GET" action="/" class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <input type="hidden" name="selected" value="{{ $image['path'] }}" />
                            <button type="submit" class="bg-blue-500 text-white px-3 py-1 rounded-md">
                                Select
                            </button>
                        </form>
                    </div>
                @endforeach
            </div>
        </div>
    </body>
</html>
