@Client.on_callback_query(filters.regex(r"^qualities#"))
async def quality_cb_handler(client: Client, query: CallbackQuery):
    _, key, offset, req = query.data.split("#")
    # 1. Get the original search string for this key
    search = BUTTONS.get(key)
    if not search:
        await query.answer("This search session expired. Please try again.", show_alert=True)
        return
    search = search.replace("_", " ")
    # 2. Gather all pages of results
    all_files = []
    current_offset = 0
    while True:
        files_page, next_offset, total = await get_search_results(search, max_results=int(MAX_BTN), offset=current_offset)
        # Convert next_offset to int safely
        try:
            next_offset = int(next_offset)
        except:
            next_offset = 0
        all_files.extend(files_page)
        if not next_offset or next_offset == current_offset:
            break
        current_offset = next_offset
    # 3. Scan all collected files for quality keywords
    found_quals = set()
    for f in all_files:
        for q in QUALITIES:
            if re.search(rf"\b{re.escape(q)}\b", f.file_name, re.IGNORECASE):
                found_quals.add(q)
    # 4. Build the quality filter buttons
    btn = [
        [InlineKeyboardButton(text=q.upper(),
            callback_data=f"quality_search#{q.lower()}#{key}#0#{offset}#{req}")]
        for q in sorted(found_quals)
    ]
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text(
        "<b>In which quality do you want the file? Choose below ↓↓</b>",
        reply_markup=InlineKeyboardMarkup(btn)
    )


@Client.on_callback_query(filters.regex(r"^languages#"))
async def languages_cb_handler(client: Client, query: CallbackQuery):
    _, key, offset, req = query.data.split("#")
    # 1. Get the original search string
    search = BUTTONS.get(key)
    if not search:
        await query.answer("This search session expired. Please try again.", show_alert=True)
        return
    search = search.replace("_", " ")
    # 2. Gather all pages of results
    all_files = []
    current_offset = 0
    while True:
        files_page, next_offset, total = await get_search_results(search, max_results=int(MAX_BTN), offset=current_offset)
        try:
            next_offset = int(next_offset)
        except:
            next_offset = 0
        all_files.extend(files_page)
        if not next_offset or next_offset == current_offset:
            break
        current_offset = next_offset
    # 3. Scan all collected files for language keywords
    found_langs = set()
    for f in all_files:
        for l in LANGUAGES:
            if re.search(rf"\b{re.escape(l)}\b", f.file_name, re.IGNORECASE):
                found_langs.add(l)
    # 4. Build the language filter buttons
    btn = [
        [InlineKeyboardButton(text=l.upper(),
            callback_data=f"lang_search#{l.lower()}#{key}#0#{offset}#{req}")]
        for l in sorted(found_langs)
    ]
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text(
        "<b>In which language do you want the file? Choose below ↓↓</b>",
        reply_markup=InlineKeyboardMarkup(btn)
    )
