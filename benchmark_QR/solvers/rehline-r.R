library(rehline)

elastic_qr = function(...)
{
    res = rehline::elastic_qr(...)
    res$beta
}
