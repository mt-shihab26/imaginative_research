<?php

use Illuminate\Support\Arr;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

function convertToBase64(string $imagePath)
{
    return $imagePath
        |> Storage::disk('local')->get(...)
        |> Str::toBase64(...);
}

Route::get('/', function () {
    $imagePaths = Storage::disk('local')->files('cat');
    $imagePaths = Arr::take($imagePaths, 10);

    $base64Images = Collection::make($imagePaths)
        ->map(fn (string $imagePath) => convertToBase64($imagePath));

    return view('welcome', [
        'images' => $base64Images,
    ]);
});
