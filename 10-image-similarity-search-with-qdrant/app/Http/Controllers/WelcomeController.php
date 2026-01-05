<?php

namespace App\Http\Controllers;

use Illuminate\Support\Arr;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class WelcomeController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $imagePaths = Storage::disk('local')->files('cat');
        $imagePaths = Arr::take($imagePaths, 10);

        $base64Images = Collection::make($imagePaths)
            ->map(fn (string $imagePath) => $this->convertToBase64($imagePath));

        return view('welcome', [
            'images' => $base64Images,
        ]);

    }

    public function convertToBase64(string $imagePath)
    {
        return $imagePath
            |> Storage::disk('local')->get(...)
            |> Str::toBase64(...);
    }
}
